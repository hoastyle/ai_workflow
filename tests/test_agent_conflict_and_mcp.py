"""
单元测试：Agent 命令冲突处理和 MCP 工具强制使用

测试改进 1️⃣: Agent 命令冲突处理
测试改进 2️⃣: MCP 工具强制使用
"""

import pytest
from unittest.mock import Mock, MagicMock
from commands.lib.agent_coordinator import AgentCoordinator
from commands.lib.agent_registry import Agent


class TestAgentCommandConflictDetection:
    """测试 detect_command_conflict 方法"""

    @pytest.fixture
    def coordinator(self):
        """创建 AgentCoordinator 实例"""
        return AgentCoordinator()

    @pytest.fixture
    def mock_agent(self):
        """创建模拟 Agent"""
        agent = Mock(spec=Agent)
        agent.name = "debug-agent"
        agent.role = "调试诊断专家"
        agent.available_tools = ["/wf_06_debug"]
        agent.match_score = 0.95
        agent.alternatives = []
        return agent

    def test_no_conflict_same_command(self, coordinator, mock_agent):
        """测试：相同命令，无冲突"""
        result = coordinator.detect_command_conflict(mock_agent, "wf_06_debug")

        assert result['has_conflict'] is False
        assert result['conflict_resolution_options'] == []

    def test_conflict_different_commands(self, coordinator, mock_agent):
        """测试：不同命令，有冲突"""
        result = coordinator.detect_command_conflict(mock_agent, "wf_04_ask")

        assert result['has_conflict'] is True
        assert len(result['conflict_resolution_options']) == 3
        assert "改用" in result['conflict_resolution_options'][0]

    def test_conflict_with_slash_prefix(self, coordinator, mock_agent):
        """测试：命令带斜杠前缀"""
        result = coordinator.detect_command_conflict(mock_agent, "/wf_04_ask")

        assert result['has_conflict'] is True

    def test_conflict_resolution_options(self, coordinator, mock_agent):
        """测试：三个选择选项的内容"""
        result = coordinator.detect_command_conflict(mock_agent, "wf_04_ask")

        options = result['conflict_resolution_options']
        assert "改用" in options[0]
        assert "继续" in options[1]
        assert "同时执行" in options[2]

    def test_empty_tools_list(self, coordinator, mock_agent):
        """测试：Agent 无可用工具"""
        mock_agent.available_tools = []
        result = coordinator.detect_command_conflict(mock_agent, "wf_04_ask")

        assert result['has_conflict'] is False
        assert result['conflict_resolution_options'] == []


class TestMCPToolRecommendations:
    """测试 extract_mcp_recommendations 方法"""

    @pytest.fixture
    def coordinator(self):
        return AgentCoordinator()

    @pytest.fixture
    def mock_agent(self):
        agent = Mock(spec=Agent)
        agent.name = "debug-agent"
        agent.role = "调试诊断专家"
        return agent

    @pytest.fixture
    def sample_mcp_hints(self):
        """样本 MCP 提示"""
        return [
            {
                'tool': 'sequential-thinking',
                'usage': '结构化错误分析',
                'confidence': 0.90,
                'priority': 'high',
                'reason': '复杂错误需要系统化分析'
            },
            {
                'tool': 'serena',
                'usage': '代码级深度定位',
                'confidence': 0.75,
                'priority': 'medium',
                'reason': '精确定位错误位置'
            },
            {
                'tool': 'tavily',
                'usage': '相似问题搜索',
                'confidence': 0.45,
                'priority': 'low',
                'reason': '查找参考解决方案'
            }
        ]

    def test_extract_high_priority_tools(self, coordinator, mock_agent, sample_mcp_hints):
        """测试：提取高优先级工具"""
        result = coordinator.extract_mcp_recommendations(mock_agent, sample_mcp_hints)

        assert result['should_enable_mcp'] is True
        assert 'sequential-thinking' in result['enabled_tools']

    def test_extract_medium_priority_tools(self, coordinator, mock_agent, sample_mcp_hints):
        """测试：提取中优先级工具"""
        result = coordinator.extract_mcp_recommendations(mock_agent, sample_mcp_hints)

        # 应该启用高 + 前2个中优先级
        assert 'serena' in result['enabled_tools']

    def test_low_priority_not_enabled(self, coordinator, mock_agent, sample_mcp_hints):
        """测试：低优先级工具不启用"""
        result = coordinator.extract_mcp_recommendations(mock_agent, sample_mcp_hints)

        assert 'tavily' not in result['enabled_tools']

    def test_tool_descriptions(self, coordinator, mock_agent, sample_mcp_hints):
        """测试：工具描述列表"""
        result = coordinator.extract_mcp_recommendations(mock_agent, sample_mcp_hints)

        descriptions = result['tool_descriptions']
        assert len(descriptions) > 0
        assert 'SEQUENTIAL-THINKING' in descriptions[0]

    def test_mcp_justification(self, coordinator, mock_agent, sample_mcp_hints):
        """测试：MCP 使用理由"""
        result = coordinator.extract_mcp_recommendations(mock_agent, sample_mcp_hints)

        # 有高优先级工具时应该使用"强烈建议"
        assert '强烈建议' in result['mcp_justification']

    def test_empty_hints(self, coordinator, mock_agent):
        """测试：空 MCP 提示"""
        result = coordinator.extract_mcp_recommendations(mock_agent, [])

        assert result['should_enable_mcp'] is False
        assert result['enabled_tools'] == []

    def test_none_agent(self, coordinator):
        """测试：None Agent"""
        result = coordinator.extract_mcp_recommendations(None, [])

        assert result['should_enable_mcp'] is False


class TestIntegration:
    """集成测试：冲突处理 + MCP 推荐"""

    @pytest.fixture
    def coordinator(self):
        return AgentCoordinator()

    def test_full_workflow(self, coordinator):
        """测试：完整的冲突处理 + MCP 推荐流程"""
        # 创建模拟 Agent
        agent = Mock(spec=Agent)
        agent.name = "debug-agent"
        agent.role = "调试诊断专家"
        agent.available_tools = ["/wf_06_debug"]
        agent.match_score = 0.95
        agent.alternatives = []

        # 创建 MCP 提示
        mcp_hints = [
            {'tool': 'sequential-thinking', 'usage': '错误分析', 'confidence': 0.85, 'priority': 'high', 'reason': 'test'},
            {'tool': 'serena', 'usage': '代码定位', 'confidence': 0.70, 'priority': 'medium', 'reason': 'test'},
        ]

        # 检测冲突
        conflict = coordinator.detect_command_conflict(agent, "wf_04_ask")
        assert conflict['has_conflict'] is True

        # 提取 MCP 推荐
        mcp_rec = coordinator.extract_mcp_recommendations(agent, mcp_hints)
        assert mcp_rec['should_enable_mcp'] is True
        assert 'sequential-thinking' in mcp_rec['enabled_tools']
        assert 'serena' in mcp_rec['enabled_tools']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
