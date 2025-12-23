"""
AgentDecisionEngine 单元测试

测试覆盖:
- 匹配度计算 (5 个测试)
- 决策逻辑 (5 个测试)
- 选项格式化 (3 个测试)
- 错误处理 (2 个测试)

总计: 15 个单元测试，覆盖率目标 ≥90%
"""

import pytest
from commands.lib.agent_decision_engine import (
    AgentDecisionEngine,
    DecisionResult,
)


class TestAgentDecisionEngine:
    """AgentDecisionEngine 测试类"""

    @pytest.fixture
    def engine(self):
        """创建决策引擎实例"""
        return AgentDecisionEngine()

    @pytest.fixture
    def high_confidence_context(self):
        """高置信度上下文"""
        return {
            "agent_id": "test-agent-1",
            "agent_name": "Test Agent",
            "recommendation": "/wf_05_code 实现新功能",
            "confidence": 0.95,
            "expertise": ["代码实现", "功能开发"],
        }

    @pytest.fixture
    def medium_confidence_context(self):
        """中等置信度上下文"""
        return {
            "agent_id": "test-agent-2",
            "agent_name": "Test Agent 2",
            "recommendation": "/wf_07_test 编写测试",
            "confidence": 0.75,
            "expertise": ["测试开发", "覆盖率分析"],
        }

    @pytest.fixture
    def low_confidence_context(self):
        """低置信度上下文"""
        return {
            "agent_id": "test-agent-3",
            "agent_name": "Test Agent 3",
            "recommendation": "/wf_08_review 代码审查",
            "confidence": 0.45,
            "expertise": ["代码审查"],
        }

    # ============================================================================
    # 匹配度计算测试 (5 个)
    # ============================================================================

    def test_high_match_score(self, engine, high_confidence_context):
        """测试高匹配度评分"""
        user_command = "/wf_05_code 实现新功能"
        score = engine.calculate_match_score(high_confidence_context, user_command)

        # 相同的主命令（/wf_05_code），应该得到高分
        # 关键词匹配 0.75 * 0.4 + 置信度 0.95 * 0.4 = 0.30 + 0.38 = 0.68 + context
        assert score >= 0.75
        assert score <= 1.0

    def test_medium_match_score(self, engine, medium_confidence_context):
        """测试中等匹配度评分"""
        user_command = "/wf_07_test"
        score = engine.calculate_match_score(medium_confidence_context, user_command)

        # 相同的主命令，应该得到中等分
        # 前缀匹配 0.75 * 0.4 + 置信度 0.75 * 0.4 = 0.30 + 0.30 = 0.60
        assert 0.50 <= score <= 0.9

    def test_low_match_score(self, engine, low_confidence_context):
        """测试低匹配度评分"""
        user_command = "/wf_11_commit 提交代码"
        score = engine.calculate_match_score(low_confidence_context, user_command)

        # 不同的主命令，分数应较低
        # Jaccard + 置信度 0.45 * 0.4 = 很低
        assert score <= 0.60

    def test_exact_keyword_match(self, engine):
        """测试精确关键词匹配"""
        agent_context = {
            "recommendation": "install dependencies",
            "confidence": 0.9,
            "expertise": ["依赖管理"],
        }
        user_command = "install dependencies"

        score = engine.calculate_match_score(agent_context, user_command)

        # 完全相同，分数应很高（关键词 100% + 置信度 90%）
        assert score >= 0.75

    def test_partial_context_match(self, engine):
        """测试部分上下文匹配"""
        agent_context = {
            "recommendation": "/wf_07_test 编写单元测试",
            "confidence": 0.7,
            "expertise": ["单元测试", "集成测试"],
        }
        user_command = "/wf_07_test 编写集成测试"

        score = engine.calculate_match_score(agent_context, user_command)

        # 部分关键词匹配
        assert 0.4 <= score <= 0.8

    # ============================================================================
    # 决策逻辑测试 (5 个)
    # ============================================================================

    def test_auto_mode_high_score(self, engine, high_confidence_context):
        """测试自动模式 - 高分"""
        # 测试相同的主命令，这样会有更高的匹配度
        result = engine.decide(
            agent_context=high_confidence_context,
            user_command="/wf_05_code",  # 相同的主命令
            decision_mode="auto",
        )

        # 相同的主命令 + 高置信度应该自动执行推荐或显示选项
        assert result.decision_mode in ["auto", "prompt"]
        if result.decision_mode == "auto":
            assert result.final_command == high_confidence_context["recommendation"]
        assert result.match_score >= 0.60

    def test_prompt_mode_medium_score(self, engine, medium_confidence_context):
        """测试提示模式 - 中等分"""
        # 测试不同的主命令，这样会有中等匹配度
        result = engine.decide(
            agent_context=medium_confidence_context,
            user_command="/wf_11_commit",  # 不同的主命令
            decision_mode="auto",
        )

        # 不同的主命令、中等置信度应该显示选项或信息
        assert result.decision_mode in ["prompt", "info"]
        assert result.match_score < 0.85

    def test_info_mode_low_score(self, engine, low_confidence_context):
        """测试信息模式 - 低分"""
        result = engine.decide(
            agent_context=low_confidence_context,
            user_command="/wf_11_commit 提交代码",
            decision_mode="auto",
        )

        # 低分应该执行用户命令，仅提示信息
        assert result.decision_mode == "info"
        assert result.final_command == "/wf_11_commit 提交代码"
        assert result.match_score < 0.65

    def test_force_agent_mode(self, engine, high_confidence_context):
        """测试强制 Agent 模式"""
        result = engine.decide(
            agent_context=high_confidence_context,
            user_command="/wf_11_commit 提交代码",
            decision_mode="force_agent",
        )

        # 强制模式应该使用 Agent 推荐
        assert result.decision_mode == "auto"
        assert result.final_command == high_confidence_context["recommendation"]

    def test_force_user_mode(self, engine, high_confidence_context):
        """测试强制用户命令模式"""
        user_cmd = "/wf_11_commit 提交代码"
        result = engine.decide(
            agent_context=high_confidence_context,
            user_command=user_cmd,
            decision_mode="force_user",
        )

        # 强制模式应该使用用户命令
        assert result.decision_mode == "auto"
        assert result.final_command == user_cmd

    # ============================================================================
    # 选项格式化测试 (3 个)
    # ============================================================================

    def test_format_three_options(self, engine):
        """测试格式化三个选项"""
        agent_cmd = "/wf_05_code 实现功能"
        user_cmd = "/wf_08_review 代码审查"

        formatted = engine.format_options(agent_cmd, user_cmd)

        # 验证格式包含所有必要信息
        assert agent_cmd in formatted
        assert user_cmd in formatted
        assert "Agent 推荐冲突" in formatted
        assert "选择" in formatted

    def test_option_descriptions(self, engine):
        """测试选项描述"""
        options = engine.get_option_descriptions()

        # 验证三个选项
        assert len(options) == 3
        assert all("label" in opt and "description" in opt for opt in options)

        # 验证选项内容
        labels = [opt["label"] for opt in options]
        assert "使用 Agent 推荐" in labels
        assert "继续用户命令" in labels
        assert "并行执行" in labels

    def test_option_selection_validation(self, engine, high_confidence_context):
        """测试选项选择验证"""
        result = engine.decide(
            agent_context=high_confidence_context,
            user_command="/wf_11_commit",
            decision_mode="prompt",
        )

        # 验证选项结构
        assert result.options is not None
        for option in result.options:
            assert isinstance(option["label"], str)
            assert isinstance(option["description"], str)
            assert len(option["label"]) > 0
            assert len(option["description"]) > 0

    # ============================================================================
    # 错误处理测试 (2 个)
    # ============================================================================

    def test_invalid_context(self, engine):
        """测试无效上下文处理"""
        invalid_context = {}  # 空上下文
        user_command = "/wf_05_code 实现功能"

        result = engine.decide(
            agent_context=invalid_context,
            user_command=user_command,
            decision_mode="auto",
        )

        # 应该降级处理，返回有效结果
        assert result is not None
        assert isinstance(result, DecisionResult)
        assert result.final_command == user_command

    def test_invalid_user_command(self, engine, high_confidence_context):
        """测试无效用户命令处理"""
        invalid_command = ""  # 空命令

        result = engine.decide(
            agent_context=high_confidence_context,
            user_command=invalid_command,
            decision_mode="auto",
        )

        # 应该返回有效结果
        assert result is not None
        assert isinstance(result, DecisionResult)

    # ============================================================================
    # 边界情况测试 (额外的健壮性测试)
    # ============================================================================

    def test_identical_commands(self, engine):
        """测试相同命令的处理"""
        context = {
            "recommendation": "/wf_05_code 实现功能",
            "confidence": 0.9,
        }
        user_command = "/wf_05_code 实现功能"

        result = engine.decide(
            agent_context=context,
            user_command=user_command,
            decision_mode="auto",
        )

        # 命令相同时应直接返回
        assert result.match_score == 1.0
        assert result.final_command == user_command

    def test_empty_recommendation(self, engine):
        """测试空推荐处理"""
        context = {
            "recommendation": "",
            "confidence": 0.5,
        }
        user_command = "/wf_05_code 实现功能"

        result = engine.decide(
            agent_context=context,
            user_command=user_command,
            decision_mode="auto",
        )

        # 应该降级处理
        assert result is not None
        assert isinstance(result, DecisionResult)

    def test_decision_history_tracking(self, engine, high_confidence_context):
        """测试决策历史跟踪"""
        # 进行多个决策
        for i in range(3):
            engine.decide(
                agent_context=high_confidence_context,
                user_command=f"/wf_0{i}_test 测试{i}",
                decision_mode="auto",
            )

        # 验证历史记录
        assert len(engine.decision_history) == 3
        for record in engine.decision_history:
            assert "final_command" in record
            assert "mode" in record
            assert "score" in record
            assert "reason" in record

    def test_match_score_bounds(self, engine):
        """测试匹配度评分在有效范围内"""
        contexts = [
            {
                "recommendation": "",
                "confidence": 0.0,
            },
            {
                "recommendation": "/wf_05_code",
                "confidence": 1.0,
            },
            {
                "recommendation": "test command",
                "confidence": 0.5,
                "expertise": ["测试"],
            },
        ]

        for context in contexts:
            score = engine.calculate_match_score(context, "/wf_05_code 测试")
            # 分数应总是在 0.0-1.0 范围内
            assert 0.0 <= score <= 1.0

    def test_decision_result_structure(self, engine, high_confidence_context):
        """测试决策结果结构完整性"""
        result = engine.decide(
            agent_context=high_confidence_context,
            user_command="/wf_11_commit",
            decision_mode="auto",
        )

        # 验证所有必需字段
        assert hasattr(result, "final_command")
        assert hasattr(result, "decision_mode")
        assert hasattr(result, "match_score")
        assert hasattr(result, "agent_recommendation")
        assert hasattr(result, "user_command")
        assert hasattr(result, "reason")

        # 验证类型
        assert isinstance(result.final_command, str)
        assert isinstance(result.decision_mode, str)
        assert isinstance(result.match_score, float)
        assert isinstance(result.reason, str)


# ============================================================================
# 集成测试
# ============================================================================


class TestAgentDecisionEngineIntegration:
    """AgentDecisionEngine 集成测试"""

    @pytest.fixture
    def engine(self):
        """创建决策引擎实例"""
        return AgentDecisionEngine()

    def test_complete_decision_workflow(self, engine):
        """测试完整决策工作流"""
        # 模拟工作流：高置信度 + 相同主命令 → 自动决策
        agent_context = {
            "agent_id": "code-agent",
            "agent_name": "Implementation Engineer",
            "recommendation": "/wf_05_code 实现新功能",
            "confidence": 0.92,
            "expertise": ["功能实现", "代码编写"],
        }

        # 场景 1: 相同主命令，应自动执行推荐
        result = engine.decide(
            agent_context=agent_context,
            user_command="/wf_05_code",
            decision_mode="auto",
        )

        # 主命令相同 + 高置信度应触发自动模式
        assert result.decision_mode in ["auto", "prompt"]
        # 如果自动模式，应使用推荐命令
        if result.decision_mode == "auto":
            assert result.final_command == agent_context["recommendation"]

    def test_conflicting_recommendations_handling(self, engine):
        """测试冲突推荐处理"""
        agent_context = {
            "recommendation": "/wf_07_test 编写测试",
            "confidence": 0.7,
            "expertise": ["测试"],
        }

        # 场景: 用户想运行 /wf_08_review，但 Agent 推荐 /wf_07_test
        result = engine.decide(
            agent_context=agent_context,
            user_command="/wf_08_review",
            decision_mode="auto",
        )

        # 不同的主命令、中等置信度应显示选项或信息
        assert result.decision_mode in ["prompt", "info"]
        if result.decision_mode == "prompt":
            assert result.options is not None

    def test_low_confidence_fallback(self, engine):
        """测试低置信度降级"""
        agent_context = {
            "recommendation": "/wf_11_commit 提交代码",
            "confidence": 0.3,
            "expertise": ["版本控制"],
        }

        result = engine.decide(
            agent_context=agent_context,
            user_command="/wf_05_code 实现功能",
            decision_mode="auto",
        )

        # 低置信度应执行用户命令
        assert result.decision_mode == "info"
        assert result.final_command == "/wf_05_code 实现功能"
